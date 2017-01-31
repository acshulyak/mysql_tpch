#!usr/bin/python

import sys
from sets import Set

inFile = open(sys.argv[1], "r")
outFile = open(sys.argv[1]+".csv", "w")

test_map = {"r003c": "Unhalted Core Cycles",
            "r00c0": "Instructions Retired",
            "r4f2e": "LLC References",
            "r412e": "LLC Misses",
            "r00c4": "Branches",
            "r00c5": "Branch Misses",
            "r01a2": "Total Resource Stalls",
            "r04a2": "RS Resource Stalls",
            "r08a2": "SB Resource Stalls",
            "r10a2": "ROB Resource Stalls",
            "r0280": "iL1 misses",
            "r08d1": "dL1 misses",
            "r8108": "dTLB Load Misses",
            "r0149": "dTLB Store Misses",
            "r0185": "iTLB Misses",
            "r2024": "L2 instruction misses",
            "r024c": "HW PF Hits for Loads",
            "r014c": "SW PF Hits for Loads",
            "r0110": "FP Instructions",
            "rf010": "SSE Instructions",
            "r0124": "L2 Read Hits",
            "r0324": "L2 Reads",
            "r0824": "L2 RFO Misses",
            "r0c24": "L2 RFOs",
            "r2024": "L2 Instruction Read Misses",
            "r3024": "L2 Instruction Reads",
            "r8024": "L2 Prefetch Misses",
            "rc024": "L2 Prefetches",
            "r0279": "IDQ.EMPTY",
            "r0480": "ICACHE.IFETCH_STALL",
            "rc189": "BR_MISP_EXEC.COND",
            "r8489": "BR_MISP_EXEC.INDIRECT_JMP_NON_CALL_RET",
            "r8889": "BR_MISP_EXEC.RETURN_NEAR",
            "r9089": "BR_MISP_EXEC.DIRECT_NEAR_CALL",
            "ra089": "BR_MISP_EXEC.INDIRECT_NEAR_CALL",
            "r019c": "IDQ_UOPS_NOT_DELIVERED.CORE",
            "r010e": "UOPS_ISSUED.ANY",
            "r04c3": "MACHINE_CLEARS.SMC",
            "r01ae": "ITLB.ITLB_FLUSH",
            "r20bd": "TLB_FLUSH.STLB_ANY",
            "r0249": "DTLB_STORE_MISSES.WALK_COMPLETED",
            "r0449": "DTLB_STORE_MISSES.WALK_DURATION",
            "r1049": "DTLB_STORE_MISSES.STLB_HIT",
            "r8208": "DTLB_LOAD_MISSES.MISS_CAUSES_A_WALK",
            "r8408": "DTLB_LOAD_MISSES.WALK_DURATION",
            "r045f": "DTLB_LOAD_MISSES.STLB_HIT",
            "r0285": "ITLB_MISSES.WALK_COMPLETED",
            "r0485": "ITLB_MISSES.WALK_DURATION",
            "r1085": "ITLB_MISSES.STLB_HIT",
            "r0151": "L1D.REPLACEMENT",
            "r01a3": "CYCLE_ACTIVITY.CYCLES_L2_PENDING",
            "r02a3": "CYCLE_ACTIVITY.CYCLES_LDM_PENDING",
            "r04a3": "CYCLE_ACTIVITY.CYCLES_NO_EXECUTE",
            "r05a3": "CYCLE_ACTIVITY.STALLS_L2_PENDING",
            "r06a3": "CYCLE_ACTIVITY.STALLS_LDM_PENDING",
            "r08a3": "CYCLE_ACTIVITY.CYCLES_L1D_PENDING",
            "r0ca3": "CYCLE_ACTIVITY.STALLS_L1D_PENDING",
            "r01c2": "UOPS_RETIRED.ALL",
            "r013c": "Unhalted Reference Cycles",
	    "r02c2": "UOPS_RETIRED.RETIRE_SLOTS",
	    "r030d": "INT_MISC.RECOVERY_CYCLES",
	    "cpu/event=0xb1,umask=0x01,cmask=1/": "UOPS_EXECUTED.THREAD:c1",
	    "cpu/event=0xb1,umask=0x01,cmask=2/": "UOPS_EXECUTED.THREAD:c2"}

results = {}
events = Set()

for line in inFile:
  line = line.strip()
  if "#" not in line and len(line) > 0:
    if "<" in line:
        print line
    line = line.split(" ")
    line = filter(None, line)
    if "<" in line[1]:
      event = line[3].split(":")
    else:
      event = line[2].split(":")
    if test_map.has_key(event[0]):
      event_name = test_map[event[0]]
    else:
      print event[0], "not a known event"
      event_name = event[0]
    if len(event) > 1:
        if event[1] == "u":
          event_name += "(user mode)"
        elif event[1] == "k":
          event_name += "(system mode)"
    events.add(event_name)
    if not results.has_key(float(line[0])):
      results[float(line[0])] = {}
    if "<" in line[1]:
      results[float(line[0])][event_name] = 0
    else:
      results[float(line[0])][event_name] = int(line[1].replace(',',''))

events = list(events)
outFile.write("time,"+",".join(events)+"\n")
order_results = sorted(results.keys())
for key in order_results:
  time_events = [str(results[key].get(event, "")) for event in events]
  outFile.write(str(key)+","+",".join(time_events)+"\n")

inFile.close()
outFile.close()

