<script>
	import { reviewState, page } from "./store.js";
	import { get } from "svelte/store";

	function showBack() {
		const state = get(reviewState);
		state.step = "back";
		reviewState.set(state);
	}

	async function reviewCard(grade) {
		const state = get(reviewState);

		let response;
		let data;

		response = await fetch("http://127.0.0.1:8000/cards/review", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				deck_id: state.deck_id,
				card_id: state.deck_id,
				grade: grade,
			}),
		});
		data = await response.json();

		response = await fetch(`http://127.0.0.1:8000/decks/${state.deck_id}/get_next`);
		data = await response.json();

		state["due_card_count"] = data.due_card_count;

		// Finished reviewing
		if (data.due_card_count == 0) {
			state.card = null;
			page.set("my_decks");
		}

		else {
			state.card = {
				front: data.front,
				back: data.back,
				id: data.card_id,
			};
		}

		state.step = "front";
		reviewState.set(state);
	}
</script>

{#if $reviewState.due_card_count == 1}
	<p>There is 1 card left to review in {$reviewState.deck_name}.</p>
{:else}
	<p>There are {$reviewState.due_card_count} cards left to review in
	{$reviewState.deck_name}.</p>
{/if}

<blockquote>
	<h3>{$reviewState.card.front}</h3>
	<hr>
	{#if $reviewState.step == "front"}
		<h3>...</h3>
	{:else}
		<h3>{$reviewState.card.back}</h3>
	{/if}
</blockquote>

<hr>

{#if $reviewState.step == "front"}
	<div id="review">
		<button on:click={showBack}>Show back</button>
	</div>
{:else}
	<p>Did you correctly recall this card?</p>

	<div id="review">
		<button on:click={() => reviewCard(4)}>Correct</button>
		<button on:click={() => reviewCard(2)} id="incorrect">Incorrect</button>
	</div>
{/if}

<style>
	h3, p {
		text-align: center;
	}

	button#incorrect {
		background-color: #C2002E;
		border-color: #C2002E;
	}

	button#incorrect:hover {
		background-color: #75001c;
		background-color: #75001c;
	}

	blockquote {
		padding: 2em;
	}

	hr {
		margin: 2em;
	}

	div#review {
		display: flex;
		justify-content: center;
		align-content: center;
		gap: 1em;
	}
</style>
