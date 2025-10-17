function display(id) {
   if (id == 'TotalProduct') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('Stock').classList.add('hide');
      document.getElementById('Sale').classList.add('hide');
            document.getElementById('staff').classList.add('hide');

      document.getElementById('TakeAway').classList.add('hide');
      document.getElementById('AddProduct').classList.add('hide');
      document.getElementById('chatbot').classList.add('hide');

   }
   else if (id == 'Stock') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('TotalProduct').classList.add('hide');
      document.getElementById('Sale').classList.add('hide');
      document.getElementById('TakeAway').classList.add('hide');
            document.getElementById('staff').classList.add('hide');

      document.getElementById('chatbot').classList.add('hide');
      document.getElementById('AddProduct').classList.add('hide');
   }
   else if (id == 'Sale') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('TotalProduct').classList.add('hide');
      document.getElementById('Stock').classList.add('hide');
      document.getElementById('TakeAway').classList.add('hide');
            document.getElementById('staff').classList.add('hide');

      document.getElementById('AddProduct').classList.add('hide');
      document.getElementById('chatbot').classList.add('hide');

   }
   else if (id == 'AddProduct') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('TotalProduct').classList.add('hide');
      document.getElementById('Stock').classList.add('hide');
      document.getElementById('TakeAway').classList.add('hide');
      document.getElementById('Sale').classList.add('hide');
            document.getElementById('staff').classList.add('hide');

      document.getElementById('chatbot').classList.add('hide');

   }

   else if (id == 'TakeAway') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('TotalProduct').classList.add('hide');
      document.getElementById('Stock').classList.add('hide');
      document.getElementById('Sale').classList.add('hide');
            document.getElementById('staff').classList.add('hide');

      document.getElementById('AddProduct').classList.add('hide');
      document.getElementById('chatbot').classList.add('hide');

   }
   else if (id == 'chatbot') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('TotalProduct').classList.add('hide');
      document.getElementById('Stock').classList.add('hide');
      document.getElementById('Sale').classList.add('hide');
      document.getElementById('TakeAway').classList.add('hide');
      document.getElementById('staff').classList.add('hide');
      document.getElementById('AddProduct').classList.add('hide');

   }
   else if (id == 'staff') {
      document.getElementById(id).classList.remove('hide');
      document.getElementById('TotalProduct').classList.add('hide');
      document.getElementById('Stock').classList.add('hide');
      document.getElementById('Sale').classList.add('hide');
      document.getElementById('TakeAway').classList.add('hide');
      document.getElementById('AddProduct').classList.add('hide');
      document.getElementById('chatbot').classList.add('hide');

   }
}


