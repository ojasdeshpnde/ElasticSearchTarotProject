
import { getBackendIP } from "./localhostSettings";

export default function getHello() {
    fetch(getBackendIP())
    .then(response => response.json())
    .then(data => console.log(data));
}

export function getTestImage() {
    fetch(getBackendIP() +  '/testimage')
    .then(response => response.json())
    .then(data => console.log(data));
}