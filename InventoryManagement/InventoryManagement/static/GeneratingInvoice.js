// const Form = document.getElementById('invoice-form');
// const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Form.addEventListener('submit', (e) => {
//     e.preventDefault();
//     const data = {
//         pname: document.getElementById("pname").value,
//         pcode: document.getElementById("pcode").value,
//         qnt: parseInt(document.getElementById("Qnt").value),
//         price: document.getElementById("price").value,
//         customerName:document.getElementById('Cname').value,
//         customerMob:document.getElementById('Cmob').value,
//         FullHalfPayemnt:document.getElementById('Full-Half').value,
//         paymentMode:document.getElementById('PaymentMode').value,
//         dueStart:document.getElementById('Startdate').value,
//         dueEnd:document.getElementById('Enddate').value,
//         PayingAmount:document.getElementById('PayingAmount').value,
//         balanceAmount:parseFloat(price)-parseFloat(PayingAmount)
//     };
//     console.log(data);
//     fetch("/GenerateInvoice/", {
//         method: 'POST',
//         body: JSON.stringify(data), headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": csrfToken,
//         },
//     })
//         .then((response)=>response.json())
//         .then((data) => {
//             if(data.status=='Success'){
//                 document.getElementById("displayInvoice").innerHTML='Success';

//             }
//             else{
//                 document.getElementById('displayInvoice').innerHTML=data.status;
//             }
//         }).catch(error => console.log('error in invoice generation'));
// })

const Sale = document.getElementById('sale');

Sale.addEventListener('click', (e) => {
  e.preventDefault();
  try {
    let name = document.getElementById('Cname').value.trim();
    let mob = document.getElementById('Cmob').value.trim();
    let full_half = document.getElementById('Full-Half').value.trim();
    let pmode = document.getElementById('PaymentMode').value.trim();

    let nameRegex = /^[A-Za-z ]+$/;
    let mobileRegex = /^[0-9]{10}$/;

    if (!name || !mob || !full_half || !pmode) {
      alert('Please Fill Customer details');
    }

    else if (!nameRegex.test(name)) {
      alert("Customer Name should only contain alphabets (no numbers or special characters).");
    }

    else if (!mobileRegex.test(mob)) {
      alert("Mobile Number must be exactly 10 digits.");
    }

    else {
      let cart = JSON.parse(localStorage.getItem("cart")) || [];
      let cname = document.getElementById("Cname").value;
      let cmob = document.getElementById("Cmob").value;
      let today = new Date().toLocaleDateString();
      let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      // Create a new window for printing
      const printWindow = window.open('', '', 'height=600,width=600');

      printWindow.document.write('<html><head><title>Invoice</title>');
      printWindow.document.write(`
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .invoice-box { max-width: 600px; padding: 20px; border: 1px solid #000; }
    .header { text-align: center; margin-bottom: 20px; }
    .header h2 { margin: 0; }
    .details { margin-bottom: 20px; }
    .details p { margin: 2px 0; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
    table, th, td { border: 1px solid black; padding: 8px; text-align: center; }
    .total { text-align: right; font-weight: bold; margin-top: 10px; }
    .footer { text-align: center; margin-top: 20px; font-style: italic; }
  </style>
`);
      printWindow.document.write('</head><body>');
      printWindow.document.write('<div class="invoice-box">');

      // Company Header
      printWindow.document.write(`
  <div class="header">
    <h2>ABC SuperMarket</h2>
    <p>123 Main Street, City</p>
    <p>Phone: 9876543210</p>
  </div>
`);

      // Customer Details
      printWindow.document.write(`
  <div class="details">
    <p><strong>Customer Name:</strong> ${cname}</p>
    <p><strong>Mobile No:</strong> ${cmob}</p>
    <p><strong>Date:</strong> ${today}</p>
  </div>
`);

      // Product Table
      printWindow.document.write(`
  <table>
    <tr>
      <th>Product Name</th>
      <th>Quantity</th>
      <th>Price</th>
      <th>Total</th>
    </tr>
`);
      let grandTotal = 0;
      cart.forEach(item => {
        let total = item.qnt * item.price;
        grandTotal += total;
        printWindow.document.write(`
    <tr>
      <td>${item.name}</td>
      <td>${item.qnt}</td>
      <td>${item.price.toFixed(2)}</td>
      <td>${total.toFixed(2)}</td>
    </tr>
  `);
      });
      printWindow.document.write('</table>');

      // Grand Total
      printWindow.document.write(`<p class="total">Grand Total: ₹${grandTotal.toFixed(2)}</p>`);

      // Footer
      printWindow.document.write(`<div class="footer">Thank you for shopping! Visit Again 🙏</div>`);

      printWindow.document.write('</div></body></html>');

      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
      printWindow.close();
      //alert(cart);
      let billinfo = {
        'cname': cname,
        'mob': cmob,
        'Total': grandTotal,
        'PaymentType':document.getElementById('Full-Half').value,
        'HalfFull':document.getElementById('PaymentMode').value,
        'items': cart
      }
      fetch("/BillingInfo/", {
        method: "POST",
        body: JSON.stringify(billinfo),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        }
      })
        .then(res => {
          if (res.ok) {    // ✅ just check status
            alert("The billing info has been saved!");
            localStorage.removeItem("cart");
            document.getElementById("cart-body").innerHTML = "";
          } else {
            alert("Billing info can't be saved");
          }
        })
        .catch(() => alert("Billing info can't be saved"));

    }
  }
  catch (err) {
    alert(err);
    console.log(err);
  }
});




//
function printInvoice() {
  // Show the invoice table
  const invoice = document.getElementById('PurchasingItem');
  invoice.style.display = 'block';

  // Create a new window for printing
  const printWindow = window.open('', '', 'height=600,width=800');

  // Add the table HTML to the new window
  printWindow.document.write('<html><head><title>Invoice</title>');
  printWindow.document.write('<style>table { width: 100%; border-collapse: collapse; } table, th, td { border: 1px solid black; padding: 8px; }</style>');
  printWindow.document.write('</head><body >');
  printWindow.document.write(invoice.innerHTML);
  printWindow.document.write('</body></html>');

  // Print and close
  printWindow.document.close();
  printWindow.focus();
  printWindow.print();
  printWindow.close();
}

