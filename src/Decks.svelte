<script>
	import { decks } from "./store.js";
</script>

<div>
	{#each $decks as deck}
		{#if deck.mine}
			<blockquote>
				<strong>{deck.name}</strong>
				<br>
				by {deck.author}

				<br>

				<button>Review</button>
				<button>Edit</button>
			</blockquote>
		{/if}
	{/each}
</div>

<style>
	div {
		display: grid;
		grid-template-columns: 1fr 1fr;
	}

	blockquote {
		margin: 1em;
	}

	button {
		margin-top: 2em;
	}
</style>
