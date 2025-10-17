document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loginForm").addEventListener("submit", async function (event) {
        event.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        let errmsg = document.getElementById("err-msg");
        try {
                errmsg.innerHTML='Validating...'
                const authResponse = await fetch("/Authenticate/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json", 
                    "X-CSRFToken":  document.querySelector("[name=csrfmiddlewaretoken]").value 
                },
                body: JSON.stringify({ email, password })
            });
            const authData = await authResponse.json();
            console.log("Auth Response:", authData);
            if (authData.success) {
                window.location.href = authData.redirect_url;
            } else {
                errmsg.innerHTML="Invalid gmail or password.";
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});


// displaying sent email status
document.getElementById('mail').addEventListener('click',(event)=>{
   event.preventDefault();
   alert('Your Low stock Mail is in Processing...');
   fetch('/mail/').then((response)=>{
      return response.json();
   }).then((obj)=>{
    alert(obj.status);    
   })
})