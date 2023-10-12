# <u><span style="color:#4682B4">Lightweight handler functions to query LLM and capture vector embeddings</span></u>

- This project has two function
  - One to get the event and do a vector embedding.
  - Second on to handle query action on the posted question based on vector embedding and running the gpt model on it.

To perform a 2-legged API call with mutual TLS in PointClickCare, you need to follow these steps:
1. Determine whether you need to use 2-legged or 3-legged OAuth based on whether users of your application have PointClickCare credentials. If your application users have PointClickCare credentials, you must use 3-legged OAuth. If they don't have PointClickCare credentials, you may use 2-legged OAuth. Reference: [Using 2-legged vs 3-legged OAuth](https://developer-qa.pointclickcare.com/spa/documentation/using-2-legged-vs-3-legged-oauth)
2. Ensure that your certificate meets the requirements specified by PointClickCare. The certificate must be fully chained, have a minimum key length of 2048-bits, be signed using SHA-2, not be in a revoked state or self-signed, and carry at least $500,000 worth of insurance coverage. Reference: [Supported Certificates](https://developer-qa.pointclickcare.com/spa/documentation/apples-1)
3. Update your application's name to the Valid Certificate Common Name to make a successful 2-legged API call. This can be done through the Account > My Apps section in PointClickCare. Reference: [Replacing the Certificate Common Name](https://developer-qa.pointclickcare.com/spa/documentation/apples-1)
4. Use the provided sample code as a reference to implement the 2-legged API call in your preferred programming language. The sample code includes examples in PHP, C#, Node.js, and Java. Reference: [Sample Code](https://developer-qa.pointclickcare.com/spa/documentation/apples-1)
5. Please note that the provided sample code is just an example, and you may need to modify it according to your specific requirements and programming environment.