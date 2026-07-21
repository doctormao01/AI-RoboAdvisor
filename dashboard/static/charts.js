document.addEventListener("DOMContentLoaded", function () {

    const pieCanvas = document.getElementById("portfolioPie");

    if (!pieCanvas) {
        return;
    }

    const labels = JSON.parse(pieCanvas.dataset.labels);
    const values = JSON.parse(pieCanvas.dataset.values);

    new Chart(pieCanvas, {

        type: "pie",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Allocazione",

                    data: values,

                    borderWidth: 1

                }

            ]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                },

                title: {

                    display: false

                }

            }

        }

    });

});