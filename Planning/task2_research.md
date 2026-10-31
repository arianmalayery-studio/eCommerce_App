# Practical Task 2: Web Technologies & API Research

## 1. Python Requests Module

### Overview
The `requests` module is a widely used Python HTTP library designed to simplify sending HTTP requests compared to standard library tools like `urllib`. It abstracts lower-level tasks such as query string encoding, connection pooling, and SSL verification behind a clear, human-readable API.

### Usage
Making HTTP requests follows direct method calls corresponding to standard HTTP verbs:
* **GET Requests:** `response = requests.get('https://api.example.com/items', params={'category': 'tech'})` queries resources, with query parameters safely encoded.
* **POST Requests:** `response = requests.post('https://api.example.com/items', json={'name': 'Widget', 'price': 19.99})` serializes Python dictionaries directly to JSON payloads.
* **Response Handling:** Status inspection (`response.status_code`), decoded text (`response.text`), parsed JSON (`response.json()`), and header reading (`response.headers`) provide structured access to server responses.

---

## 2. Data Formats: JSON vs. XML

### Overview
* **JSON (JavaScript Object Notation):** A text-based, lightweight data-interchange format composed of key-value pairs and ordered lists, primarily used in REST APIs and web services.
* **XML (Extensible Markup Language):** A tag-based markup language that defines rules for encoding documents in a format that is both human- and machine-readable, commonly used in enterprise services (SOAP) and document storage.

### Advantages & Disadvantages

| Data Format | Advantages | Disadvantages |
| :--- | :--- | :--- |
| **JSON** | 1. Lightweight and minimal payload overhead.<br>2. Native parsing support in modern programming languages and JavaScript engines.<br>3. Intuitive structure directly mapping to arrays and objects/dictionaries.<br>4. High parsing speed with lower compute/memory resource consumption. | 1. No native support for comments.<br>2. Limited native data typing (lacks dates, binary data types).<br>3. Schema validation (JSON Schema) is optional and less standardized than XML schemas.<br>4. Lacks namespaces, leading to naming collisions across complex domain integrations. |
| **XML** | 1. Strong schema validation via XSD and DTD.<br>2. Namespace support to prevent element naming conflicts in multi-system systems.<br>3. Advanced querying and transformation capabilities using XPath and XSLT.<br>4. Capable of representing mixed content (tags interspersed within arbitrary text). | 1. High verbosity due to repetitive opening and closing tags.<br>2. Slower parsing speed and larger memory footprint.<br>3. More complex parsing APIs (DOM and SAX models).<br>4. Susceptible to XML External Entity (XXE) vulnerabilities if parsers are misconfigured. |

---

## 3. RESTful APIs

### Overview
A RESTful API (Representational State Transfer) is an architectural style for networked systems that leverages standard HTTP protocols to perform operations on resources identified by URIs.

### How It Works
* **Stateless Communication:** Every request contains all necessary credentials and parameters; the server stores no client session context.
* **Uniform Interface:** Standard HTTP verbs correspond to CRUD actions:
  * `GET`: Retrieve resource
  * `POST`: Create resource
  * `PUT` / `PATCH`: Update resource
  * `DELETE`: Remove resource
* **Standard Status Codes:** Communicates outcome via HTTP status codes (e.g., `200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `500 Internal Server Error`).

### Advantages & Disadvantages

#### Advantages:
1. **Stateless Scalability:** Stateless requests allow easy horizontal scaling across load-balanced application instances.
2. **Platform & Language Independence:** Clients and servers can use entirely different languages and frameworks as long as they adhere to the HTTP interface.
3. **Cacheability:** Standardized HTTP cache headers (`Cache-Control`, `ETag`) optimize network usage and improve response times.
4. **Standardized Tooling:** Built on top of standard web protocols, enabling use of existing proxies, firewalls, and debugging tools without bespoke configurations.

#### Disadvantages:
1. **Over-fetching & Under-fetching:** Endpoints return fixed data structures, requiring clients to either retrieve unnecessary fields or trigger multiple round-trips for related resources.
2. **Stateless Overhead:** Transporting headers, authentication tokens, and metadata in every standalone request increases transmission overhead.
3. **Lack of Real-Time Bi-Directional Streaming:** Inefficient for high-frequency, bidirectional real-time communications compared to WebSockets or gRPC.
4. **Endpoint Proliferation:** Large enterprise architectures can develop hundreds of disjointed endpoints that demand rigorous documentation and maintenance.
