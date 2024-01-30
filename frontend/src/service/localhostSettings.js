

export  function getBackendIP(){
    return 'http://localhost:' + getPort()
}


function getPort(){
    return '5002';
}