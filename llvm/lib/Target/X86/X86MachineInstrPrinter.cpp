#include "X86.h"
#include "X86InstrInfo.h"
#include "llvm/CodeGen/MachineFunctionPass.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"

using namespace llvm;

#define X86_MACHINEINSTR_PRINTER_PASS_NAME "Dummy X86 machineinstr printer pass"
#define DEBUG_TYPE "X86MachineInstrPrinter"

namespace {

class X86MachineInstrPrinter : public MachineFunctionPass {
public:
  static char ID;

  X86MachineInstrPrinter() : MachineFunctionPass(ID) {
    initializeX86MachineInstrPrinterPass(*PassRegistry::getPassRegistry());
  }

  bool runOnMachineFunction(MachineFunction &MF) override;

  StringRef getPassName() const override { return X86_MACHINEINSTR_PRINTER_PASS_NAME; }
private:
  bool isPrintable(MachineFunction &MF);
};

char X86MachineInstrPrinter::ID = 0;

bool X86MachineInstrPrinter::isPrintable(MachineFunction &MF) {
  return MF.getFunction().getFnAttribute(Attribute::AttrKind::YourAttribute).isValid();
}

bool X86MachineInstrPrinter::runOnMachineFunction(MachineFunction &MF) {
  if (!isPrintable(MF)) {
    return false;
  }
  LLVM_DEBUG(dbgs() << MF.getName() << "\n");
  for (auto &MBB : MF) {
    LLVM_DEBUG(dbgs() << "Contents of MachineBasicBlock:\n");
    LLVM_DEBUG(dbgs() << MBB << "\n");
    const BasicBlock *BB = MBB.getBasicBlock();
    LLVM_DEBUG(dbgs() << "Contents of BasicBlock corresponding to MachineBasicBlock:\n");
    LLVM_DEBUG(dbgs() << BB << "\n");

    LLVM_DEBUG(dbgs() << BB->getName() << "\n");

    LLVM_DEBUG(dbgs() << "[\n");
    for (auto &instr: BB->getInstList()) {
      LLVM_DEBUG(dbgs() << instr << "\n");
    }
    LLVM_DEBUG(dbgs() << "]\n");
  }

  return false;
}

} // end of anonymous namespace

INITIALIZE_PASS(X86MachineInstrPrinter, "x86-machineinstr-printer",
                X86_MACHINEINSTR_PRINTER_PASS_NAME,
                true, // is CFG only?
                true  // is analysis?
)

namespace llvm {

FunctionPass *createX86MachineInstrPrinter() { return new X86MachineInstrPrinter(); }

}