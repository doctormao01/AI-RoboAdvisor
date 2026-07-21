document.addEventListener("DOMContentLoaded", () => {

    const saveButton = document.getElementById("saveButton");
    const updateButton = document.getElementById("updateButton");
    const capitalInput = document.getElementById("capital");

    // ----------------------------
    // Salva impostazioni
    // ----------------------------

    if (saveButton) {

        saveButton.addEventListener("click", async () => {

            const capital = parseFloat(capitalInput.value);

            if (isNaN(capital) || capital <= 0) {
                alert("Inserisci un capitale valido.");
                return;
            }

            saveButton.disabled = true;
            saveButton.innerHTML = "💾 Salvataggio...";

            try {

                const response = await fetch("/save_settings", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        capital: capital
                    })
                });

                const result = await response.json();

                if (result.success) {

                    alert("✅ Impostazioni salvate.");

                    location.reload();

                } else {

                    alert("Errore durante il salvataggio.");

                }

            } catch (err) {

                console.error(err);

                alert("Errore di connessione con il server.");

            } finally {

                saveButton.disabled = false;
                saveButton.innerHTML = "💾 Salva impostazioni";

            }

        });

    }

    // ----------------------------
    // Aggiorna dati ETF
    // ----------------------------

    if (updateButton) {

        updateButton.addEventListener("click", async () => {

            updateButton.disabled = true;
            updateButton.innerHTML = "⏳ Aggiornamento...";

            try {

                const response = await fetch("/update_data", {
                    method: "POST"
                });

                const result = await response.json();

                if (result.success) {

                    alert("🚀 Aggiornamento avviato.\n\nLa dashboard verrà aggiornata automaticamente tra pochi secondi.");

                    setTimeout(() => {

                        location.reload();

                    }, 5000);

                } else {

                    alert("Errore durante l'aggiornamento.");

                }

            } catch (err) {

                console.error(err);

                alert("Errore di connessione.");

            } finally {

                updateButton.disabled = false;
                updateButton.innerHTML = "🔄 Aggiorna dati";

            }

        });

    }

});