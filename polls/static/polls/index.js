const form = document.getElementById('form');
const username = document.getElementById('username');
const password = document.getElementById('password');

form.addEventListener('submit', e =>{
   let messages =[]
   if (username.value === '' ||username.value == null){
    messages.push('Username is required.')
   }

   if (password.value === '' || password.value == null){
    messages.push('Password  is required.')
   }

   if(password.value.length >= 20){
    messages.push('Password must be lesser than 20 characters.')
   }

   if(password.value === 'password'){
    messages.push('Password can not be set as Password')
   }

   if(password.value === '1234'){
    messages.push('1234 is definately not a Password')
   }

   if (messages.length > 0){
    e.preventDefault();
    errorElement.innerText = messages.join(',')
   }
});


function updatePollAnimation() {
  const voteElements = document.querySelectorAll('.vote');
  
  voteElements.forEach(voteElement => {
    const percentage = parseFloat(voteElement.querySelector('.vote-count').textContent);
    
    if (!isNaN(percentage) && percentage >= 0 && percentage <= 100) {
      const containerWidth = voteElement.querySelector('.container').clientWidth;
      const blueWidth = (percentage / 100) * containerWidth;
      const redWidth = containerWidth - blueWidth;
  
      voteElement.querySelector('.blue').style.width = blueWidth + 'px';
      voteElement.querySelector('.red').style.width = redWidth + 'px';
    }
  });
}

// Call the function initially
updatePollAnimation();

// Periodically check for changes in the vote count (e.g., every second)
setInterval(updatePollAnimation, 1000);


