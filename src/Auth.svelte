<script>
	import { user, page } from "./store.js";
	import { get } from "svelte/store";

	let username = "";
	let password = "";

	let url = "";

	page.subscribe(() => {
		// Clear when switching pages
		username = "";
		password = "";

		url = {
			"login": "http://127.0.0.1:8000/login",
			"register": "http://127.0.0.1:8000/register"
		}[get(page)];
		console.log(url);
	})

	async function submit() {
		const response = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				username: username,
				password: password
			})
		});

		const data = await response.json();
		const id = data["user_id"];

		if (id) {
			user.set({id: id, username: username});
			page.set("home");
		}
		else {
			alert("Error authenticating");
			console.log(data);
		}
	}
</script>

<label for="username">Username</label>
<input id="username" bind:value={username}>

<label for="password">Password</label>
<input id="password" type="password" bind:value={password}>

<br>

<button on:click={submit}>Submit</button>
