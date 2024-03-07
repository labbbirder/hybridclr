#pragma once

#include "InterpreterDefs.h"

namespace hybridclr
{

namespace interpreter
{

	extern const char* visiting_field;
	class Interpreter
	{
	public:

		static void Execute(const MethodInfo* methodInfo, StackObject* args, void* ret);

	};

}
}

