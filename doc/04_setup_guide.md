# Setup Document (Running the Sandbox)

To launch this sandbox and prove the concept to leadership on your local machine:

1. **Start the Environment:**
   Run the following command in your terminal from the root repository directory:
   ```bash
   docker compose up --build -d
   ```
2. **Access the Dashboard:**
   Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)**. 
   *(Credentials: `admin` / `admin`)*
3. **View the Magic:**
   You will instantly see the QA API Coverage dashboard tracking simulated real-world traffic against simulated QA tests.

To stop the sandbox, run:
```bash
docker compose down
```
