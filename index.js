const loadBooks = () => {
    const xhttp = new XMLHttpRequest();

    xhttp.open("GET", "http://localhost:3000/books", false);
    xhttp.send();

    const books = JSON.parse(xhttp.responseText);

    for (let book of books) {
        const x = `
                <div class="card">
                        <h1>${book.restroname}</h1>
                        <h2>Dish: ${book.dish}</h2>
                        <h3>Food Quantity: ${book.quantity}</h3>
                        <h4>Optional Description/Message: ${book.desc}</h4>
                        <p>Time: ${book.time}</p>
                        <button onclick={twilioSend()}>Remind ME!</button>
                </div>
        `

        document.getElementById('books').innerHTML = document.getElementById('books').innerHTML + x;
    }
}
loadBooks();