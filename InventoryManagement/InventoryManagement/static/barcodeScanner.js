const input = document.getElementById("barcodeInput");
const ProductName = document.getElementById('ProductName');
const Quantity = document.getElementById('Qnt');
const Pcode = document.getElementById('Pcode');
const Price = document.getElementById('Price');
let PerPrice = '';
document.addEventListener("DOMContentLoaded", (event) => {
  event.preventDefault();
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      const barcode = input.value.trim();
      console.log(barcode);
      fetch(`/getData/${barcode}/`, { method: 'GET' })
        .then((response) => response.json())
        .then((data) => {
          if (data.item.length === 0) {
            document.getElementById('displayInvoice').textContent = "No item found for this barcode.";
          } else {
            const [name, quantity, price] = data.item[0];
            if(quantity<10){
                input.value='';
                document.getElementById('displayInvoice').innerHTML = "Item out of stock";
            
              }
            if(quantity>10){
            console.log("Setting values:", name, quantity, price);
            ProductName.value = name;
            Quantity.value = 1;
            Price.value = parseFloat(price);
            PerPrice = parseFloat(price);
            Pcode.value = '';
          }
        }
        })
        .catch(error => {
          console.log("Error fetching data.");
        });

    }
  })
});

Quantity.addEventListener('change', () => {
  totalQnt = Quantity.value;
  GrandTotal = parseInt(totalQnt) * parseFloat(PerPrice);
  console.log(GrandTotal);
  Price.value = parseFloat(GrandTotal);
})


const FullHalfPayemnt = document.getElementById('Full-Half');
FullHalfPayemnt.addEventListener('change', () => {
  let duedate = document.getElementsByClassName('DueDate');
  // let PayingAmount = document.getElementById('PayingAmount');
  let TotalAmount = document.getElementById('Price');
  if (FullHalfPayemnt.value == 'HalfPayment') {
    duedate[0].classList.remove('hide');
    let today = new Date();
    today.setDate(today.getDate() + 7);
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0');
    let yyyy = today.getFullYear();

    let nextWeek = yyyy + '-' + mm + '-' + dd;  // Correct format
    document.getElementById("duedate").value = nextWeek;
    // duedate[1].classList.remove('hide');
    // duedate[2].classList.remove('hide');
    // PayingAmount.value = parseFloat(TotalAmount.value) / 2;
    // console.log(`${PayingAmount.value}`);
    // console.log(`${TotalAmount.value}`);


  }
  else {
    duedate[0].classList.add('hide');
    duedate[1].classList.add('hide');
    duedate[2].classList.add('hide');
  }
});


// Add product to cart (localStorage)
function addProduct(barcode, name, qnt, price) {

  let cart = JSON.parse(localStorage.getItem("cart")) || [];

  // Check if already exists
  let existing = cart.find(p => p.bc === barcode);

  if (existing) {
    existing.qnt += qnt;
    existing.total = existing.qnt * existing.price;
  } else {
    cart.push({
      bc: barcode,
      name: name,
      price: price,
      qnt: qnt,
      total: qnt * price
    });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  displayCart();
}

// Display cart in the table
function displayCart() {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let tbody = document.getElementById("cart-body");
  tbody.innerHTML = "";
  let halPayment;
  cart.forEach(item => {
    let row = document.createElement("tr");
    row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.qnt}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>${item.total.toFixed(2)}</td>
        `;
    tbody.appendChild(row);
    halPayment += item.total;
  });
  // document.getElementById("PayingAmount").value=halPayment/2;
}

// Handle ScanNext button
document.getElementById("scanNext").addEventListener("click", function (e) {
  e.preventDefault();

  let barcode = document.getElementById("barcodeInput").value.trim();
  let name = document.getElementById("ProductName").value.trim();
  let qnt = parseInt(document.getElementById("Qnt").value.trim());
  let price = parseFloat(document.getElementById("Price").value.trim());

  // Validation: make sure fields are filled correctly
  if (!barcode || !name || isNaN(qnt) || qnt <= 0 || isNaN(price) || price <= 0) {
    alert("⚠️ Please fill all fields with valid values.");
    console.log([barcode, name, qnt, price]);
    return;
  }

  // Add to cart
  addProduct(barcode, name, qnt, price);

  // Clear input fields
  document.getElementById("barcodeInput").value = "";
  document.getElementById("ProductName").value = "";
  document.getElementById("Qnt").value = "";
  document.getElementById("Price").value = "";
});

// Load cart on page load
displayCart();



