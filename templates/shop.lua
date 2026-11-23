--!strict
-- Template: shop (boutique StudGrid, style "Studs Chunky")
-- Modelled on: docs/previews/shop-chunky.html (validated at the preview gate).
-- Official references (create.roblox.com):
--   /docs/en-us/production/game-design/ui-ux-design.md : coin bundles give visual priority
--     to the highest-value bundle (Dragon Adventures, https://www.roblox.com/games/3475397644/);
--     close button square, top-right, dialogs (same doc).
--   /docs/en-us/ui/9-slice.md, /docs/en-us/ui/appearance-modifiers.md : UICorner for corners,
--     UIStroke Border mode for outlines, UIGradient for gradients.
--   /docs/en-us/production/publishing/accessibility.md : UITextSizeConstraint bounds text.
-- Measured from the preview (not from a game capture): panel padding 14 px, corner 14 px,
--   outline 4 px, hard shadow 5 px down-right (zero blur), buy button 48 px high,
--   header 64 px, gutter 16 px.
--
-- Signature: return function(parent: Instance, tokens: {}): Instance
-- tokens may override palette keys and set `content` (see Content type below).

export type Tokens = {
	ink: Color3,
	goldTop: Color3,
	goldBottom: Color3,
	cream: Color3,
	greenTop: Color3,
	greenBottom: Color3,
	coin: Color3,
	danger: Color3,
	backdrop: Color3,
	content: Content?,
}

export type Item = { name: string, desc: string, price: number, limited: boolean?, onBuy: (() -> ())? }
export type Lootbox = { name: string, desc: string, price: number, odds: { { label: string, percent: number } }, onOpen: (() -> ())? }
export type Content = { lootbox: Lootbox?, items: { Item } }

local TweenService = game:GetService("TweenService")
local FONT = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Heavy)

local DEFAULT: Tokens = {
	ink = Color3.fromHex("0B120F"),
	goldTop = Color3.fromHex("FFD23F"),
	goldBottom = Color3.fromHex("E0A800"),
	cream = Color3.fromHex("FFF6D6"),
	greenTop = Color3.fromHex("76CC7B"),
	greenBottom = Color3.fromHex("4FA95A"),
	coin = Color3.fromHex("FFC93C"),
	danger = Color3.fromHex("E4574C"),
	backdrop = Color3.fromHex("2B6E3A"),
	content = nil,
}

local STROKE = 4
local SHADOW = 5
local RADIUS = 14
local PAD = 14
local BUY_HEIGHT = 48
local HEADER_H = 64
local CLOSE_SIZE = 48
local GUTTER = 16

local function corner(parent: Instance, radius: number)
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, radius)
	c.Parent = parent
end

local function outline(parent: Instance, ink: Color3)
	local s = Instance.new("UIStroke")
	s.Color = ink
	s.Thickness = STROKE
	s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
	s.Parent = parent
end

-- Hard shadow: a sibling ink frame placed BEHIND the surface, offset down-right, no blur.
local function hardShadow(surface: GuiObject, ink: Color3, radius: number)
	local shadow = Instance.new("Frame")
	shadow.Name = surface.Name .. "Shadow"
	shadow.Size = surface.Size
	shadow.Position = surface.Position + UDim2.fromOffset(SHADOW, SHADOW)
	shadow.AnchorPoint = surface.AnchorPoint
	shadow.BackgroundColor3 = ink
	shadow.BorderSizePixel = 0
	shadow.ZIndex = surface.ZIndex - 1
	corner(shadow, radius)
	shadow.Parent = surface.Parent
	return shadow
end

-- Layout-safe surface: a transparent wrapper (the layout child) holds the ink shadow
-- and the surface. The shadow is inside the wrapper so UIListLayout/UIGridLayout
-- never see it as a separate cell.
local function wrapSurface(parent: Instance, t: Tokens, name: string, size: UDim2, fill: Color3, radius: number): Frame
	local wrap = Instance.new("Frame")
	wrap.Name = name .. "Wrap"
	wrap.Size = size
	wrap.BackgroundTransparency = 1
	wrap.BorderSizePixel = 0
	local inset = UDim2.new(1, -SHADOW, 1, -SHADOW)

	local shadow = Instance.new("Frame")
	shadow.Name = "HardShadow"
	shadow.Size = inset
	shadow.Position = UDim2.fromOffset(SHADOW, SHADOW)
	shadow.BackgroundColor3 = t.ink
	shadow.BorderSizePixel = 0
	corner(shadow, radius)
	shadow.Parent = wrap

	local f = Instance.new("Frame")
	f.Name = name
	f.Size = inset
	f.BackgroundColor3 = fill
	f.BorderSizePixel = 0
	corner(f, radius)
	outline(f, t.ink)
	f.Parent = wrap

	wrap.Parent = parent
	return f
end

local function surface(parent: Instance, t: Tokens, name: string, size: UDim2, fill: Color3): Frame
	return wrapSurface(parent, t, name, size, fill, RADIUS)
end

local function label(parent: Instance, text: string, color: Color3, min: number, max: number): TextLabel
	local l = Instance.new("TextLabel")
	l.BackgroundTransparency = 1
	l.FontFace = FONT
	l.Text = text
	l.TextColor3 = color
	l.TextScaled = true
	l.TextWrapped = true
	l.Parent = parent
	local c = Instance.new("UITextSizeConstraint")
	c.MinTextSize = min
	c.MaxTextSize = max
	c.Parent = l
	return l
end

-- Price: coin icon + number, never bare text.
local function priceRow(parent: Instance, t: Tokens, amount: number, color: Color3): Frame
	local row = Instance.new("Frame")
	row.Name = "Price"
	row.BackgroundTransparency = 1
	row.Size = UDim2.new(1, 0, 0, 26)
	local layout = Instance.new("UIListLayout")
	layout.FillDirection = Enum.FillDirection.Horizontal
	layout.VerticalAlignment = Enum.VerticalAlignment.Center
	layout.Padding = UDim.new(0, 8)
	layout.SortOrder = Enum.SortOrder.LayoutOrder
	layout.Parent = row

	local coin = Instance.new("Frame")
	coin.Name = "Coin"
	coin.Size = UDim2.fromOffset(24, 24)
	coin.BackgroundColor3 = t.coin
	coin.BorderSizePixel = 0
	coin.LayoutOrder = 1
	corner(coin, 12)
	outline(coin, t.ink)
	coin.Parent = row

	local amountLabel = label(row, tostring(amount), color, 14, 22)
	amountLabel.Name = "Amount"
	amountLabel.Size = UDim2.new(0, 0, 1, 0)
	amountLabel.AutomaticSize = Enum.AutomaticSize.X
	amountLabel.LayoutOrder = 2
	row.Parent = parent
	return row
end

-- Buy button: the single accent of the screen. Verb left, price right, no overlap.
local function buyButton(parent: Instance, t: Tokens, verb: string, amount: number, onClick: (() -> ())?): TextButton
	local b = Instance.new("TextButton")
	b.Name = "Buy"
	b.Size = UDim2.new(1, -SHADOW, 1, -SHADOW)
	b.BackgroundColor3 = t.greenTop
	b.BorderSizePixel = 0
	b.AutoButtonColor = false
	b.Text = ""
	corner(b, 12)
	outline(b, t.ink)
	local grad = Instance.new("UIGradient")
	grad.Color = ColorSequence.new(t.greenTop, t.greenBottom)
	grad.Rotation = 90
	grad.Parent = b

	local wrap = Instance.new("Frame")
	wrap.Name = "BuyWrap"
	wrap.Size = UDim2.new(1, 0, 0, BUY_HEIGHT + SHADOW)
	wrap.BackgroundTransparency = 1
	local shadow = Instance.new("Frame")
	shadow.Name = "HardShadow"
	shadow.Size = UDim2.new(1, -SHADOW, 1, -SHADOW)
	shadow.Position = UDim2.fromOffset(SHADOW, SHADOW)
	shadow.BackgroundColor3 = t.ink
	shadow.BorderSizePixel = 0
	corner(shadow, 12)
	shadow.Parent = wrap
	b.Parent = wrap
	wrap.Parent = parent

	local row = Instance.new("Frame")
	row.Name = "Row"
	row.BackgroundTransparency = 1
	row.Size = UDim2.fromScale(1, 1)
	row.Parent = b
	local pad = Instance.new("UIPadding")
	pad.PaddingLeft = UDim.new(0, PAD)
	pad.PaddingRight = UDim.new(0, PAD)
	pad.Parent = row

	local verbLabel = label(row, verb, t.cream, 14, 20)
	verbLabel.Size = UDim2.fromScale(0.55, 1)
	verbLabel.TextXAlignment = Enum.TextXAlignment.Left
	verbLabel.Parent = row

	local priceFrame = priceRow(row, t, amount, t.ink)
	priceFrame.Size = UDim2.fromScale(0.45, 1)
	priceFrame.Position = UDim2.fromScale(0.55, 0)
	priceFrame.AnchorPoint = Vector2.zero
	priceFrame.ZIndex = b.ZIndex
	local layout = priceFrame:FindFirstChildOfClass("UIListLayout") :: UIListLayout
	layout.HorizontalAlignment = Enum.HorizontalAlignment.Right

	b.Activated:Connect(function()
		-- 120-180 ms press motion, ease-out.
		TweenService:Create(b, TweenInfo.new(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
			Position = UDim2.fromOffset(2, 2),
		}):Play()
		if onClick then
			onClick()
		end
	end)
	return b
end

-- Event ribbon: rotated, overlapping the panel edge.
local function ribbon(parent: Instance, t: Tokens, text: string)
	local r = Instance.new("TextLabel")
	r.Name = "Ribbon"
	r.AnchorPoint = Vector2.new(1, 0)
	r.Position = UDim2.new(1, 8, 0, -14)
	r.Size = UDim2.fromOffset(120, 28)
	r.BackgroundColor3 = t.danger
	r.BorderSizePixel = 0
	r.Rotation = -6
	r.FontFace = FONT
	r.Text = text
	r.TextColor3 = Color3.new(1, 1, 1)
	r.TextScaled = true
	r.ZIndex = parent.ZIndex + 2
	corner(r, 8)
	outline(r, t.ink)
	r.Parent = parent
	local c = Instance.new("UITextSizeConstraint")
	c.MinTextSize = 12
	c.MaxTextSize = 16
	c.Parent = r
end

local function lootboxCard(parent: Instance, t: Tokens, box: Lootbox)
	local card = surface(parent, t, "Lootbox", UDim2.new(1, 0, 0, 230), t.cream)
	card.LayoutOrder = 0
	local inner = Instance.new("Frame")
	inner.BackgroundTransparency = 1
	inner.Size = UDim2.fromScale(1, 1)
	inner.Parent = card
	local pad = Instance.new("UIPadding")
	pad.PaddingTop = UDim.new(0, PAD)
	pad.PaddingBottom = UDim.new(0, PAD)
	pad.PaddingLeft = UDim.new(0, PAD)
	pad.PaddingRight = UDim.new(0, PAD)
	pad.Parent = inner
	local list = Instance.new("UIListLayout")
	list.Padding = UDim.new(0, 8)
	list.SortOrder = Enum.SortOrder.LayoutOrder
	list.Parent = inner

	local title = label(inner, box.name, t.ink, 18, 28)
	title.Size = UDim2.new(1, 0, 0, 30)
	title.TextXAlignment = Enum.TextXAlignment.Left
	title.LayoutOrder = 1
	title.Parent = inner

	local desc = label(inner, box.desc, t.ink, 14, 18)
	desc.Size = UDim2.new(1, 0, 0, 40)
	desc.TextXAlignment = Enum.TextXAlignment.Left
	desc.LayoutOrder = 2
	desc.Parent = inner

	-- Odds always shown in %: never hidden.
	local odds = Instance.new("Frame")
	odds.Name = "Odds"
	odds.BackgroundColor3 = Color3.new(1, 1, 1)
	odds.BorderSizePixel = 0
	odds.Size = UDim2.new(1, 0, 0, 80)
	odds.LayoutOrder = 3
	corner(odds, 10)
	outline(odds, t.ink)
	odds.Parent = inner
	local oddsList = Instance.new("UIListLayout")
	oddsList.SortOrder = Enum.SortOrder.LayoutOrder
	oddsList.Parent = odds
	for i, row in box.odds do
		local line = label(odds, row.label .. "  " .. tostring(row.percent) .. " %", t.ink, 14, 18)
		line.Size = UDim2.new(1, 0, 0, 20)
		line.TextXAlignment = Enum.TextXAlignment.Left
		line.LayoutOrder = i
	end

	local buy = buyButton(inner, t, "Ouvrir", box.price, box.onOpen)
	buy.LayoutOrder = 4
	ribbon(card, t, "NOUVEAU !")
end

local function itemCard(parent: Instance, t: Tokens, item: Item, order: number)
	local card = surface(parent, t, "Item" .. order, UDim2.new(1, 0, 0, 230), t.cream)
	card.LayoutOrder = order
	local inner = Instance.new("Frame")
	inner.BackgroundTransparency = 1
	inner.Size = UDim2.fromScale(1, 1)
	inner.Parent = card
	local pad = Instance.new("UIPadding")
	pad.PaddingTop = UDim.new(0, PAD)
	pad.PaddingBottom = UDim.new(0, PAD)
	pad.PaddingLeft = UDim.new(0, PAD)
	pad.PaddingRight = UDim.new(0, PAD)
	pad.Parent = inner
	local list = Instance.new("UIListLayout")
	list.Padding = UDim.new(0, 8)
	list.SortOrder = Enum.SortOrder.LayoutOrder
	list.Parent = inner

	local title = label(inner, item.name, t.ink, 16, 22)
	title.Size = UDim2.new(1, 0, 0, 26)
	title.TextXAlignment = Enum.TextXAlignment.Left
	title.LayoutOrder = 1
	title.Parent = inner

	local desc = label(inner, item.desc, t.ink, 14, 18)
	desc.Size = UDim2.new(1, 0, 0, 40)
	desc.TextXAlignment = Enum.TextXAlignment.Left
	desc.LayoutOrder = 2
	desc.Parent = inner

	local buy = buyButton(inner, t, "Acheter", item.price, item.onBuy)
	buy.LayoutOrder = 3
	if item.limited then
		ribbon(card, t, "LIMITÉ")
	end
end

return function(parent: Instance, tokens: {}): Instance
	local t: Tokens = {} :: any
	for k, v in DEFAULT do
		(t :: any)[k] = v
	end
	for k, v in tokens do
		(t :: any)[k] = v
	end

	local root = Instance.new("Frame")
	root.Name = "Shop"
	root.Size = UDim2.fromScale(1, 1)
	root.BackgroundColor3 = t.backdrop
	root.BorderSizePixel = 0
	root.Parent = parent
	local rootPad = Instance.new("UIPadding")
	rootPad.PaddingTop = UDim.new(0, GUTTER)
	rootPad.PaddingBottom = UDim.new(0, GUTTER)
	rootPad.PaddingLeft = UDim.new(0, GUTTER)
	rootPad.PaddingRight = UDim.new(0, GUTTER)
	rootPad.Parent = root

	-- Header: gold gradient, large bold title, square close button top-right.
	local header = surface(root, t, "Header", UDim2.new(1, 0, 0, HEADER_H), t.goldTop)
	local hgrad = Instance.new("UIGradient")
	hgrad.Color = ColorSequence.new(t.goldTop, t.goldBottom)
	hgrad.Rotation = 90
	hgrad.Parent = header
	local title = label(header, "BOUTIQUE STUDGRID", t.ink, 18, 40)
	title.Size = UDim2.new(1, -(CLOSE_SIZE + 40), 1, 0)
	title.Position = UDim2.fromOffset(PAD, 0)
	title.TextXAlignment = Enum.TextXAlignment.Left
	local close = Instance.new("TextButton")
	close.Name = "Close"
	close.Size = UDim2.fromOffset(CLOSE_SIZE, CLOSE_SIZE)
	close.AnchorPoint = Vector2.new(1, 0.5)
	close.Position = UDim2.new(1, -8, 0.5, 0)
	close.BackgroundColor3 = t.danger
	close.BorderSizePixel = 0
	close.Text = "X"
	close.TextColor3 = Color3.new(1, 1, 1)
	close.TextScaled = true
	close.FontFace = FONT
	corner(close, 10)
	outline(close, t.ink)
	close.Parent = header
	hardShadow(close, t.ink, 10)

	-- Body: lootbox first, then item grid (2 columns on phone, 3 on desktop).
	local body = Instance.new("ScrollingFrame")
	body.Name = "Body"
	body.Position = UDim2.new(0, 0, 0, HEADER_H + 18)
	body.Size = UDim2.new(1, 0, 1, -(HEADER_H + 18))
	body.BackgroundTransparency = 1
	body.BorderSizePixel = 0
	body.ScrollBarThickness = 6
	body.AutomaticCanvasSize = Enum.AutomaticSize.Y
	body.CanvasSize = UDim2.new()
	body.Parent = root
	local bodyList = Instance.new("UIListLayout")
	bodyList.Padding = UDim.new(0, GUTTER)
	bodyList.SortOrder = Enum.SortOrder.LayoutOrder
	bodyList.Parent = body

	local content: Content? = t.content
	if content then
		if content.lootbox then
			lootboxCard(body, t, content.lootbox)
		end
		local grid = Instance.new("Frame")
		grid.Name = "Grid"
		grid.BackgroundTransparency = 1
		grid.Size = UDim2.new(1, 0, 0, 0)
		grid.AutomaticSize = Enum.AutomaticSize.Y
		grid.LayoutOrder = 1
		grid.Parent = body
		local g = Instance.new("UIGridLayout")
		g.CellSize = UDim2.new(0.48, 0, 0, 230)
		g.CellPadding = UDim2.fromOffset(GUTTER, GUTTER)
		g.SortOrder = Enum.SortOrder.LayoutOrder
		g.Parent = grid
		for i, item in content.items do
			itemCard(grid, t, item, i)
		end
	end

	return root
end
