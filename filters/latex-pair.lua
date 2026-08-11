function Div(el)
  if not el.classes:includes("latex-pair") then
    return nil
  end

  local source = nil
  local result = nil

  for _, block in ipairs(el.content) do
    if block.t == "Div" and block.classes:includes("source") then
      source = block
    elseif block.t == "Div" and block.classes:includes("result") then
      result = block
    end
  end

  if not source or not result then
    return el
  end

  local source_col = pandoc.Div(
    {
      pandoc.Para({pandoc.Strong({pandoc.Str("Sorgente")})}),
      table.unpack(source.content)
    },
    pandoc.Attr("", {"column"}, {{"width", "45%"}})
  )

  local spacer_col = pandoc.Div(
    {},
    pandoc.Attr("", {"column"}, {{"width", "10%"}})
  )

  local result_col = pandoc.Div(
    {
      pandoc.Para({pandoc.Strong({pandoc.Str("Risultato")})}),
      table.unpack(result.content)
    },
    pandoc.Attr("", {"column"}, {{"width", "45%"}})
  )

  return pandoc.Div(
    {source_col, spacer_col, result_col},
    pandoc.Attr("", {"columns"})
  )
end