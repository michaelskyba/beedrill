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
		{/if}
	{/each}
</div>

<style>
	div {
		display: grid;
		grid-template-columns: 1fr 1fr;
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
