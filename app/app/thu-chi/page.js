import { getAll } from "@/lib/db";
import { PAGES } from "@/lib/pages-config";
import { PageHeader } from "@/app/components/ui";
import FinanceView from "@/app/components/FinanceView";

export const dynamic = "force-dynamic";

export default async function Page() {
  const rows = await getAll("cong_khai_thu_chi");
  return (
    <>
      <PageHeader page={PAGES["thu-chi"]} />
      <FinanceView rows={rows} />
    </>
  );
}
