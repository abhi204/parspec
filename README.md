
# Parspec assignment  

## Example API requests

- fetch metrics: https://noisy-resonance-9695.ploomber.app/metrics (GET request)
Sample request: `curl -X GET https://noisy-resonance-9695.ploomber.app/metrics`
Sample response: `{"avg_processing_time":"5.5263","pending_count":10,"processed_count":19,"processing_count":1,"total_orders":30}`

 
- create order: https://noisy-resonance-9695.ploomber.app/create_order (POST request)
Sample request: `curl -X POST https://noisy-resonance-9695.ploomber.app/create_order -H "Content-Type: application/json" -d '{
"user_id": 1,
"item_ids": [1, 2, 3, 4, 5],
"total_amount": 1234
}'`
Sample response:
`{'message': 'Order created successfully!', 'data': {"user_id": 1, "item_ids": [1, 2, 3, 4, 5], "total_amount": 1234}}`

## Design:
 A Flask application exposes the endpoints. Each web app worker has an in-memory queue and a processor thread to handle the queue data and update the database. Using a uWSGI web server, multiple workers run independently, each with its own queue and processor thread to handle orders.

**Pros:**
-   Scalable by increasing the number of workers, which increases the number of queues and processors.

**Cons:**
-   Simple architecture that may need refactoring to scale web service workers and queues independently.

## Assumptions:
Order_id is auto assigned by the database and isn't passed via the create order api payload to ensure we don't have duplicate ids.

## Public API endpoints:
- https://noisy-resonance-9695.ploomber.app/metrics (GET request)
- https://noisy-resonance-9695.ploomber.app/create_order (POST request)
- https://noisy-resonance-9695.ploomber.app/get_order/2460 (GET request)

- The client.py file included in the project can be used to make simultaneous api requests. Example: `python client.py --num_requests=10`


## SQL schema (Auto created by SQLAlchemy ORM)
```
Field			Type		Null	   Key	    Default	     Extra
---------------------------------------------------------------------
'id'			'int'		'NO'	   'PRI'	NULL		 'auto_increment'
'user_id'		'int'		'NO'	   ''		NULL		 ''
'total_amount'	'float'		'NO'	   ''		NULL		 ''
'status'		'enum('PENDING','PROCESSING','COMPLETED')'	 'NO'	''	NULL	''
'item_ids'		'varchar'	'NO'	   ''		NULL		 ''
'created_at'	'datetime'	'YES'	   ''	    'now()'	     'DEFAULT_GENERATED'
'started_at'	'datetime'	'YES'	   ''		NULL		 ''
'completed_at'	'datetime'	'YES'	   ''		NULL		 ''
```