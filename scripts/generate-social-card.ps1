Add-Type -AssemblyName System.Drawing

$outputPath = Join-Path $PSScriptRoot "..\public\assets\img\jesareko-social-card.png"
$bitmap = [System.Drawing.Bitmap]::new(1200, 630)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$background = [System.Drawing.ColorTranslator]::FromHtml("#F4F8F5")
$green = [System.Drawing.ColorTranslator]::FromHtml("#0F6B3F")
$dark = [System.Drawing.ColorTranslator]::FromHtml("#10261C")
$muted = [System.Drawing.ColorTranslator]::FromHtml("#365347")
$white = [System.Drawing.Color]::White
$graphics.Clear($background)

$greenBrush = [System.Drawing.SolidBrush]::new($green)
$darkBrush = [System.Drawing.SolidBrush]::new($dark)
$mutedBrush = [System.Drawing.SolidBrush]::new($muted)
$whiteBrush = [System.Drawing.SolidBrush]::new($white)
$graphics.FillRectangle($greenBrush, 0, 0, 34, 630)
$graphics.FillRectangle($greenBrush, 82, 82, 106, 106)

$logoFont = [System.Drawing.Font]::new("Arial", 58, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$brandFont = [System.Drawing.Font]::new("Arial", 42, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$titleFont = [System.Drawing.Font]::new("Georgia", 64, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$metaFont = [System.Drawing.Font]::new("Arial", 28, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)

$graphics.DrawString("J", $logoFont, $whiteBrush, 115, 100)
$graphics.DrawString("JESAREKO", $brandFont, $greenBrush, 218, 105)
$graphics.DrawString("Redes WiFi, CCTV y", $titleFont, $darkBrush, 82, 246)
$graphics.DrawString("soporte técnico", $titleFont, $darkBrush, 82, 327)
$graphics.DrawString("Encarnación · Itapúa · Atención personalizada", $metaFont, $mutedBrush, 86, 470)

$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$logoFont.Dispose()
$brandFont.Dispose()
$titleFont.Dispose()
$metaFont.Dispose()
$greenBrush.Dispose()
$darkBrush.Dispose()
$mutedBrush.Dispose()
$whiteBrush.Dispose()
$graphics.Dispose()
$bitmap.Dispose()
