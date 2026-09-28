import { getAll } from "@/lib/db";
import { PAGES } from "@/lib/pages-config";
import { PageHeader, Flash } from "@/app/components/ui";
import NewsList from "@/app/components/NewsList";

export const dynamic = "force-dynamic";

export default async function Page({ searchParams }) {
  const rows = await getAll("thongbao");
  return (
    <>
      <PageHeader page={PAGES["bang-tin"]} />
      <Flash searchParams={searchParams} />
      <NewsList rows={rows} />
    </>
  );
}
