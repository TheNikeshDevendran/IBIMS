document.querySelector('#SingleItem').addEventListener("submit", function (event) {
        event.preventDefault();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const data = {
        pname: document.getElementById("pname").value,
        pcode: document.getElementById("pcode").value,
        pqnt: parseInt(document.getElementById("pqnt").value),
        price: document.getElementById("price").value
        }
         fetch("/AddItem/", {
        method: 'POST',
        body: JSON.stringify(data), headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
    })
        .then((response)=>response.json())
        .then((data) => {
                    alert(data.status);
        })
    })


document.querySelector('#uploadExcel').addEventListener("submit", function (event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData();

    const fileInput = document.getElementById("File");
    formData.append("dataSheet", fileInput.files[0]);

    fetch("/AddProduct/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken,  // CSRF required for Django
        },
    })
    .then((response) => response.json())
    .then((data) => {
        alert('stocks updated');
        // document.getElementById("exl-msg").innerHTML = data.status;
    });
});



