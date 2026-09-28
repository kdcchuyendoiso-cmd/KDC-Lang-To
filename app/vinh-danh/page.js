import { getAll } from "@/lib/db";
import { PAGES } from "@/lib/pages-config";
import { PageHeader } from "@/app/components/ui";
import HonorsList from "@/app/components/HonorsList";

export const dynamic = "force-dynamic";

export default async function Page() {
  const rows = await getAll("vinh_danh");
  return (
    <>
      <PageHeader page={PAGES["vinh-danh"]} />
      <HonorsList rows={rows} />
    </>
  );
}
