import { getAll } from "@/lib/db";
import { PAGES } from "@/lib/pages-config";
import { Flash, PageHeader } from "@/app/components/ui";
import MarketView from "@/app/components/MarketView";

export const dynamic = "force-dynamic";

export default async function Page({ searchParams }) {
  const rows = await getAll("cho_que");
  return (
    <>
      <PageHeader page={PAGES["cho-que"]} />
      <Flash searchParams={searchParams} />
      <MarketView rows={rows} initialTab={searchParams?.tab} />
    </>
  );
}
