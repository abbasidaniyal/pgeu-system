# Invoices & Payments

All payments in the system are centered around the concept of
invoices. No payments are processed outside of invoices.

An invoice can be manually created, in which case nothing special
happens once it's paid. It can also be attached to an Invoice
Processor, which is then activated upon payment. Separate portions of
the system like conference registration, sponsorship or membership,
each have their own Invoice Processor. The Invoice Processor is
independent of how the invoice is handled.

If enabled, all invoices generate automatic [accounting](accounting)
records as they are completed. No accounting entries are done at
invoice issuing, only at completion.

## Flagging invoices as paid

Invoices paid to the primary bank account, or otherwise confirmed to
be in the system but not handled by the automated methods, can be
flagged as paid using the invoice administration system. In this case,
the administrator is assumed to have validated all details.

## Payment methods

A number of different automated payment methods can be supported
simultaneously in the system. This is made up of Invoice Payment
Methods, which are instances of Payment Method Implementations.

Each Invoice Payment Method has an internal name which is used in all
the administration pages, and a Name which is used in all public
facing one. For example, there can me multiple different methods
called Credit Card in the public system, but having different names in
administration in order to differentiate them (which makes sense as
long as not more than one is enabled for any given invoice).

Individual parts of the system, like conference registration and
membership can select which payment methods can be used for this
particular system. For example, some methods are more or less
appropriate for costs that are high and low.

The following fields can be configured on all payment methods:

Name
:  The name of the payment method used externally

Internal name
:  The name of the payment method used in administration pages

Active
:  Whether this method can be used. Since an invoice method that has
at some point been used cannot be deleted (due to foreign keys), it
should instead be Disabled if it should not be used.

Sort key
:  Value representing how to sort this method when multiple ones are
showed.

Implementation class
:  Reference to the underlying implementation class for this payment
method. Cannot be changed, only viewed.

### Payment implementations

The following payment implementations are available

#### Dummy payment

This method is only used for testing. All payments will be approved by
the user just clicking a button. Will only function if DEBUG is
enabled in the installation.

#### BankTransfer

This is a simple manual bank transfer, with no automation. It is
configured with a django template that will get rendered to show a
static page to the person paying the invoice, which should contain all
the bank details. All processing is handled completely manually.

#### Paypal

This method allows the payment using either a Paypal account or a
Creditcard.

Once connected to a Paypal account it will download and manage all
transactions on this account. This means that if the account is also
used for other things, those transactions will be imported and
generate warnings about not matching.

Instructions for how to fill out the Paypal integration fields are in
the form.

It requires a Return URL to be configured in Paypal. Once the method
has been created, information about this will be visible at the bottom
of the configuration page.

#### Adyen Creditcard

This method is for Creditcard payments using Adyen. This is a fairly
complex setup, but very capable. It uses a mix of direct validation,
notifications, and downloaded reports to track all the stages of a
payment. It's particularly suitable if a fairly large number of
transactions are expected.

The system is using Adyens "Hosted Payment Pages" service, which means
that all the actual processing happens at Adyen, thus not requiring a
PCI certified installation.

There are numerous steps to configure it. Much of the details needs to
be set up according to the Adyen manuals. The integration points are
all documented on the form itself.

#### Adyen Banktransfer

This is a special version of the Adyen processing. It requires there
to be a master setup using Adyen Creditcard (though it doesn't have to
be used), and it always uses the same Adyen Merchant Account as that
one. The Creditcard provider will specifically identify the IBAN
transfers as they arrive and route them to this processor.

It's set up as a separate processor due to the slowness of IBAN, and
will disable itself 5 days ahead of an invoice expiring. This is to
make it less likely that an invoice is canceled while the asynchronous
payment is being processed.

Note that with this payment method, the IBAN number and payment
details, including the reference number, is handled entirely by
Adyen. There is no way to view them from the administration side, or
the Adyen backend, and new ones are generated if one returns to the
payment page.

#### Braintree Creditcard

This method uses the Braintree creditcard gateway. Unlike the Adyen
system, this is a semi-hosted system, where the payment interface is
loaded though javascript from the Braintree systems, but the page
itself hosted as part of the system.

This module requires the Python module `braintree` to be installed.

#### Trustly Banktransfer

This method uses the Trustly system for online bank
payments. Basically it allows for payments from a regular bank
account, logged in using internet banking, without most of the
downsides of IBAN transfer. The amount is guaranteed to be correct,
and most payments complete within seconds. It is, however, limited in
which banks are supported.

As PostgreSQL Europe has a deal with Trustly that processes all
payments without fees, there is currently no support for fees in the
system. If somebody without such a deal wants to use the provider,
this should be added.

## Currencies

The system can only support one currency, globally, at any given
time. This is specified in the `local_settings.py` file, and should
normally never be changed. If it's changed once there is data in the
system, things will break.