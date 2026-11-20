import type * as Rust from './rust-derived';
import type * as Sdk from './sdk/execDiagnostics';
import type { ThreadError } from './sdk/events';

declare const rustObservation: Rust.ExecErrorObservation;
declare const sdkObservation: Sdk.ExecErrorObservation;
const observationToSdk: Sdk.ExecErrorObservation = rustObservation;
const observationToRust: Rust.ExecErrorObservation = sdkObservation;
declare const rustBinding: Rust.ExecBindingObservation;
declare const sdkBinding: Sdk.ExecBindingObservation;
const bindingToSdk: Sdk.ExecBindingObservation = rustBinding;
const bindingToRust: Rust.ExecBindingObservation = sdkBinding;
declare const rustError: Rust.ThreadErrorEvent;
declare const sdkError: ThreadError;
const errorToSdk: ThreadError = rustError;
const errorToRust: Rust.ThreadErrorEvent = sdkError;
void [observationToSdk, observationToRust, bindingToSdk, bindingToRust, errorToSdk, errorToRust];
