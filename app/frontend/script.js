function login() {
  const email = document.getElementById('email').value;
  if (!email) {
    alert('Please enter your email');
    return;
  }

  // Fake API call to fetch profit
  fetch(`http://localhost:8000/profit/${email}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('User not found');
      }
      return response.json();
    })
    .then(data => {
      document.getElementById('profit').textContent = `$${data.profit.toFixed(2)}`;
      document.getElementById('dashboard').style.display = 'block';
    })
    .catch(error => {
      alert(error.message);
    });
}
