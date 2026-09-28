import { getAll } from "@/lib/db";
import { PAGES } from "@/lib/pages-config";
import { PageHeader } from "@/app/components/ui";
import ContactsList from "@/app/components/ContactsList";

export const dynamic = "force-dynamic";

export default async function Page() {
  const rows = await getAll("danhba_thon");
  return (
    <>
      <PageHeader page={PAGES["danh-ba"]} />
      <ContactsList rows={rows} />
    </>
  );
}
