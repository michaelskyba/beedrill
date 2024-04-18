<script>
	import { myDecks } from "./store.js";

	let deckName;

	async function newDeck() {
		if (!deckName)
			return;

		alert(deckName)
	}
</script>

<div>
	{#each $myDecks as deck}
		<blockquote>
			<strong>{deck.name}</strong>
			<hr>

			{#if deck.due_cards == 0}
				<p>There are no due cards.</p>
				<button disabled>Review</button>
			{:else}
				<p>Due cards: <span class="due">{deck.due_cards}</span></p>
				<button>Review</button>
			{/if}

			<button>Edit</button>
		</blockquote>
	{/each}
</div>

<hr>

<input placeholder="Deck name" bind:value={deckName}>
<button on:click={newDeck}>Create new deck</button>

<style>
	div {
		display: grid;
		grid-template-columns: 1fr 1fr;
		max-height: 25em;
		overflow-y: scroll;
	}

	span.due {
		color: #007559;
	}

	blockquote {
		margin: 1em;
	}

	button {
		margin-top: 2em;
	}
</style>
