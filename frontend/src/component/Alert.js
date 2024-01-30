import Alert from 'react-bootstrap/Alert';

export default function AlertCom(props){

    return(
        <div>
            <Alert variant={props.loginAlertType}>
                <Alert.Heading>{props.loginAlertTitle}</Alert.Heading>
                <p>{props.loginAlertText}</p>
            </Alert>
        </div>
    );
}