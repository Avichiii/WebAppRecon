const submitElement = document.querySelector('.js-search');
submitElement.addEventListener('click', () => {
    const domainNameElement = document.querySelector('.js-search-box').value;

    fetch('/api',{
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({
            domainName: domainNameElement
        })
    })
    .then(response => {
        if (!response.ok)
            throw new Error('Network Error!!!');
        return response.text();
    })
    .then(html => {
        document.body.innerHTML = html;
    })
    .catch(error => {
        console.log(error);
    })

});


function showTab(tab) {
    document.querySelectorAll('.results').forEach(div => div.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
}

// Default tab
showTab('whois');