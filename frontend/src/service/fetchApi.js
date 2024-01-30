

export default function getHello() {
    fetch('http://localhost:5001/')
    .then(response => response.json())
    .then(data => console.log(data));
}
