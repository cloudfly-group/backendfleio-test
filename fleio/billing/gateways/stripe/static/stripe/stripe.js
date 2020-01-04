(function FleioStripe() {
    "use strict";
    document.addEventListener("DOMContentLoaded", function paymentRedirect() {
        showStripe();
    });

    function showStripe() {
        var config = JSON.parse(document.getElementsByTagName('body')[0].getAttribute('data-js-vars') || '{}');
        var stripe = Stripe(config.publicKey);

        // Create an instance of Elements
        var elements = stripe.elements();

        // Custom styling can be passed to options when creating an Element.
        // (Note that this demo uses a wider set of styles than the guide below.)
        var style = {
            base: {
                color: '#32325d',
                lineHeight: '18px',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };

        // Create an instance of the card Element
        var card = elements.create('card', {style: style});

        // Add an instance of the card Element into the `card-element` <div>
        card.mount('#card-element');

        // Handle real-time validation errors from the card Element.
        card.addEventListener('change', function (event) {
            var displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });

        // Handle form submission
        var form = document.getElementById('payment-form');
        if (form) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                stripe.createToken(card).then(function (result) {
                    if (result.error) {
                        // Inform the user if there was an error
                        var errorElement = document.getElementById('card-errors');
                        errorElement.textContent = result.error.message;
                    } else {
                        var tkfrm = document.getElementById('tokenSubmitForm');
                        var tkfield = document.getElementById('id_token');
                        tkfield.value = JSON.stringify(result.token);
                        tkfrm.submit();
                    }
                });
            });
        } else {
            form = document.getElementById('payment-form-recurring');
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                var cardButton = document.getElementById('card-button');
                var clientSecret = cardButton.dataset.secret;
                stripe.handleCardPayment(clientSecret, card).then(function (result) {
                    if (result.error) {
                        // Inform the user if there was an error
                        var errorElement = document.getElementById('card-errors');
                        errorElement.textContent = result.error.message;
                    } else {
                        if (result['paymentIntent']['status'] !== 'succeeded') {
                            console.error('Could not pay.');
                            return;
                        }
                        var recurPaymentsForm = document.getElementById('recurSubmitForm');
                        var paymentIntentField = document.getElementById('id_payment_intent');
                        paymentIntentField.value = JSON.stringify(result['paymentIntent']);
                        recurPaymentsForm.submit();
                    }
                });
            });
        }
    }
})();
