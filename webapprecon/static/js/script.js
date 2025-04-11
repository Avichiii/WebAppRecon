const submitElement = document.querySelector('.js-search');

submitElement.addEventListener('click', () => {
    const domainNameElement = document.querySelector('.js-search-box').value;

    const loaderIcon = document.getElementById('loader-icon');
    const loaderText = document.getElementById('loader-text');

    if (loaderIcon) loaderIcon.style.display = 'inline';
    if (loaderText) loaderText.textContent = ' Processing domain info...';

    fetch('/api', {
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
        if (loaderIcon) loaderIcon.style.display = 'none';
        if (loaderText) loaderText.textContent = '✅ Completed! Redirecting...';

        setTimeout(() => {
            document.body.innerHTML = html;
        }, 800);
    })
    .catch(error => {
        if (loaderIcon) loaderIcon.style.display = 'none';
        if (loaderText) loaderText.textContent = '❌ Error: ' + error.message;
        console.log(error);
    });
});

// Manage Switching between Tabs
function showTab(tab) {
    document.querySelectorAll('.slide').forEach(div => div.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
}

// Default tab
showTab('whois');