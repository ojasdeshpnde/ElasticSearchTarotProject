

export default function getHello() {
    fetch('http://localhost:5002/')
    .then(response => response.json())
    .then(data => console.log(data));
}

export function getTestImage() {
    fetch('http://localhost:5001/testimage')
    .then(response => response.json())
    .then(data => console.log(data));
}