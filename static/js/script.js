const form = document.getElementById('comment-form');

form.addEventListener('submit', e => {
    e.preventDefault();

    buildList();
});


const buildList = async () => {
    let response = await fetch('/api/comments/');
    let data = await response.json();
    console.log(data)
}

buildList();