<script>
	import { page, editingDeck } from "./store.js";
	import { get } from "svelte/store";

	let front;
	let back;

	let cards = [];

	async function getCards() {
		cards = [
			{
				id: 1,
				front: "front1",
				back: "back1",
			},
			{
				id: 2,
				front: "front2",
				back: "back2",
			},
		];

		// TODO backend
	}

	page.subscribe(v => {
		if (v == "edit_deck")
			getCards();
	});

	async function createCard() {
		const response = await fetch("http://127.0.0.1:8000/cards/add", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				deck_id: get(editingDeck).id,
				front: front,
				back: back,
			}),
		});

		front = "";
		back = "";

		const data = await response.json();
		console.log(data);

		getCards();
	}
</script>

{#if cards.length == 0}
	<p>{$editingDeck.name} has no cards yet.</p>
{:else}
	<p>{$editingDeck.name} has {cards.length} cards.</p>
{/if}

<input placeholder="Front" bind:value={front}>
<input placeholder="Back" bind:value={back}>
<button on:click={createCard}>Add</button>

{#if cards.length > 0}
	{#each cards as card}
		<blockquote>
			<p>{card.front}</p>
			<hr>
			<p>{card.back}</p>
			<hr class="half">

			<button>Delete</button>
		</blockquote>
	{/each}
{/if}

<style>
	hr.half {
		width: 25%;
		margin-left: 0;
	}
</style>
