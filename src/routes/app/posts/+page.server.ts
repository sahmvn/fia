import { db } from '$lib/server/db';
import { postsTable } from '$lib/server/db/schema';
import { desc } from 'drizzle-orm';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const posts = await db
		.select({
			id: postsTable.id,
			title: postsTable.title,
			body: postsTable.body,
			when_created: postsTable.when_created
		})
		.from(postsTable)
		.orderBy(desc(postsTable.when_created));

	return { posts };
};
