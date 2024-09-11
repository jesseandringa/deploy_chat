import { useEffect } from "react";
import './style/PayPal.css';
import {
	PayPalScriptProvider,
	PayPalButtons,
	usePayPalScriptReducer
} from "@paypal/react-paypal-js";

const ButtonWrapper = ({ type, onSubscriptionComplete }) => {
	const [{ options }, dispatch] = usePayPalScriptReducer();

    useEffect(() => {
        dispatch({
            type: "resetOptions",
            value: {
                ...options,
                intent: "subscription",
            },
        });
    }, [type]); 

	return (
        <PayPalButtons
            createSubscription={(data, actions) => {
                return actions.subscription
                    .create({
                        //test plan id
                        // plan_id: "P-3RX065706M3469222L5IFM4I",
                        plan_id: "P-3NX83087TR3419613M3QK27A", // Replace with your production plan ID
                    })
                    .then((subscriptionId) => {
                        return subscriptionId;
                    });
            }}
            onApprove={(data, actions) => {
                onSubscriptionComplete(data);
            }}
            style={{
                label: "subscribe",
            }}
        />
    );
}

export default function PayPal({onClose, onSubscriptionComplete}) {
	return (
        <div className="modal">
            <div className="modal-content">
                <h2 className="modal-title">Subscription</h2>
                <p className="modal-description">
                    Subscribe to our service to unluck unlimited access to our chatbot. Only $15 per month. 
                </p>
                <p className="modal-description">
                    You can cancel anytime.
                </p>
                <PayPalScriptProvider
                    options={{
                        clientId: "AdixsAyO8gXlkrVXj0bnzoUFR4nAda4F3wBVB5uOPgJm_5Va-6QZCLvH_x2HtRPRgdInCjGBRBfpOacl", // Replace with your live client ID
                        //sandbox client id
                        // clientId: "test",
                        components: "buttons",
                        intent: "subscription",
                        vault: true,
                    }}
                >
                    <button className="closeButton" onClick={onClose}>Close</button>
                    <ButtonWrapper type="subscription" onSubscriptionComplete={onSubscriptionComplete}/>
                </PayPalScriptProvider>
            </div>
        </div>
	);
}
