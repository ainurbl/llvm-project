#include "X86.h"
#include "X86InstrInfo.h"
#include "llvm/CodeGen/MachineFunctionPass.h"
#include "llvm/CodeGen/MachineInstrBuilder.h"

using namespace llvm;

#define X86_MACHINEINSTR_PRINTER_PASS_NAME "Dummy X86 machineinstr printer pass"

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
  outs() << MF.getName() << "\n";
  for (auto &MBB : MF) {
    outs() << "Contents of MachineBasicBlock:\n";
    outs() << MBB << "\n";
    const BasicBlock *BB = MBB.getBasicBlock();
    outs() << "Contents of BasicBlock corresponding to MachineBasicBlock:\n";
    outs() << BB << "\n";

    outs() << BB->getName() << "\n";
    outs() << "Listik\n";
    for (auto &instr: BB->getInstList()) {
      outs() << instr << "\n";
    }

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