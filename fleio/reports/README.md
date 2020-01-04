Monthly billing reporting
=========================

This Django app is here only for views and serializers if any required and the main journal_report file

Reports are generates in the journal_report file, by going through each journal entry to see the money flow
to either credit or items (services) on invoices.

Each billing plugin (for example OpenStack) has the get_service_report method which receives a service and
a start and end date. Using this information more details can be added to the report.
In the case of OpenStack, the location_cost property will contain the locations and their total cost for
the service being called for.

The report contains services and for each service we have **entries**
An *entry* is a direct payment for this service (in the case of an invoice that has the service as an item).

The total revenue for this service is the total sum of all entries.

The total_from_credit is the total usage taken from the existing customer's credit.

The **details** section, contains plugin specific details which should in turn contain the **location_cost** attribute.

Using that attribute, once can determine the cost per region for a service and the total revenu per region/location for
all services.

To obtain this result, both process_client_cron.py and generate_report should be executed.

Example

```json

{
    "revenue_report": [
        {
            "client": 679545,
            "client_display_name": "Fleio (Client name)",
            "services_report": {
                "305815": {
                    "service_name": "Shared small",
                    "service_id": 305815,
                    "entries": [
                        {
                            "amount": 5.0,
                            "item_type": "service",
                            "from_credit": false,
                            "taxes_amount": 0.0,
                            "taxes_percent": 0.0,
                            "source": "tr",
                            "date": "2019-03-01 14:21:43.969120+00:00"
                        }
                    ],
                    "fixed_monthly_price": 5.0,
                    "price_overridden": false,
                    "total_revenue": 5.0,
                    "total_from_credit": 0.0,
                    "usage_details": {},
                    "cost_still_required": 0.0,
                    "cost_required_percent": 0.0,
                    "alloted_from_credit": 0.0,
                    "debt": 0.0
                },
                "762786": {
                    "service_name": "OpenStack Project",
                    "service_id": 762786,
                    "entries": [
                        {
                            "amount": 5.0,
                            "item_type": "service",
                            "from_credit": false,
                            "taxes_amount": 0.0,
                            "taxes_percent": 0.0,
                            "source": "tr",
                            "date": "2019-03-01 11:17:51.508168+00:00"
                        }
                    ],
                    "fixed_monthly_price": 0.0,
                    "price_overridden": false,
                    "total_revenue": 5.0,
                    "total_from_credit": 0.0,
                    "usage_details": {
                        "name": "OpenStack resources report",
                        "locations": {
                            "Winterfell": {
                                "instance": {
                                    "resource_name": "Instance",
                                    "price": 51.6,
                                    "num_resources": 5
                                },
                                "volume": {
                                    "resource_name": "Volume",
                                    "price": 38.2,
                                    "num_resources": 1
                                }
                            },
                            "Riverrun": {
                                "instance": {
                                    "resource_name": "Instance",
                                    "price": 17.7,
                                    "num_resources": 3
                                }
                            }
                        },
                        "service": 762786,
                        "location_cost": {
                            "Winterfell": 89.8,
                            "Riverrun": 17.7
                        },
                        "total_cost": 107.5
                    },
                    "cost_still_required": 102.5,
                    "cost_required_percent": 100.0,
                    "alloted_from_credit": 45.0,
                    "debt": 57.5
                }
            },
            "credit_in": 45.0,
            "credit_out": 0.0,
            "credit_available": 45.0,
            "total_debt": 57.5,
            "total_alloted_from_credit": 45.0,
            "revenue_per_location": [
                {
                    "name": "Chicago",
                    "revenue": 5.0
                },
                {
                    "name": "Winterfell",
                    "revenue": 25.0
                },
                {
                    "name": "Riverrun",
                    "revenue": 25.0
                }
            ]
        }
    ],
    "total_revenue_per_location": [
        {
            "name": "Chicago",
            "revenue": 5.0
        },
        {
            "name": "Winterfell",
            "revenue": 25.0
        },
        {
            "name": "Riverrun",
            "revenue": 25.0
        }
    ],
    "total_revenue": 55.0,
    "currency_code": "EUR",
    "start_date": "2018-03-10 18:00:00+00:00",
    "end_date": "2019-03-10 18:00:00+00:00"
}
```
