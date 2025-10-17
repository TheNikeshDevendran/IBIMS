document.getElementById("CreateStaff").addEventListener('click',(e)=>{
    e.preventDefault();
    let name=document.getElementById("name").value.trim();
    let email=document.getElementById("email").value.trim();
    let password=document.getElementById("password").value.trim();
  let nameRegex = /^[A-Za-z\s]+$/;
    if (!name) {
        alert("Name is required");
        return;
    } else if (!nameRegex.test(name)) {
        alert("Name should not contain special characters or numbers");
        return;
    }

    // Email validation
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
        alert("Email is required");
        return;
    } else if (!emailRegex.test(email)) {
        alert("Enter a valid email address");
        return;
    }

    // Password validation
    if (!password) {
        alert("Password is required");
        return;
    } else if (password.length < 8) {
        alert("Password must be at least 8 characters long");
        return;
    }
  fetch('/Staff/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // for Django
    },
    body: JSON.stringify({
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value.trim(),
        role: "staff"  // or dynamic role
    })
})
.then(response => response.json())
.then(data => {
    name.value='';
    email.value='';
    password.value='';
    role.value='';
    alert(data.message);
})
.catch(error => console.error('Error:', error));

})