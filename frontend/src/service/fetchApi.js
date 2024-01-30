

export default function getHello() {
    fetch('http://localhost:' + getPort())
    .then(response => response.json())
    .then(data => console.log(data));
}

export function getTestImage() {
    fetch('http://localhost:' + getPort() +  '/testimage')
    .then(response => response.json())
    .then(data => console.log(data));
}

export function getBackendIP(){
    return 'http://localhost:' + getPort()
}


function getPort(){
    return '5002';
}
