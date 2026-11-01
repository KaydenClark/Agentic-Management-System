// The empty fixture: an empty array per planned series. This is the honest
// state until S-006 and S-002 write real rows (DDR-000T).
import type { RowsBySeries } from "../data";

export const emptyRows: RowsBySeries = {
  "held-out-per-task": [],
  "held-out-per-version": [],
  "dev-per-task": [],
  "dev-per-version": [],
};
