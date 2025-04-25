
async function registerUser() {
    const data = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      contact: document.getElementById("contact").value
    };

    try {
      const response = await fetch("/register_portal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message);
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error("Request failed:", error);
    }
  }
