    click_humano(page, "#generateBtn", "Generar informe final")
    contestado = False
    for _ in range(50):
        boton = page.query_selector("button:visible")
        if boton and boton.inner_text().strip() == "Continuar":
            boton.click()
            contestado = True
            break
        page.wait_for_timeout(500)
    if contestado:
        print("  [AVISO] Se contesto el aviso previo a generar pulsando Continuar.", flush=True)
    else:
        print("  [AVISO] El aviso previo a generar NO aparecio.", flush=True)