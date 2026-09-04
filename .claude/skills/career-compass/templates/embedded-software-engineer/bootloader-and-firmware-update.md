---
title: "Bootloader and Firmware Update Mechanism"
track: "embedded-software-engineer"
difficulty_tier: "advanced"
estimated_hours: 16
role: "core"
skill_tags: ["firmware-updates", "cryptography-basics", "c-cpp", "microcontrollers", "embedded-debugging"]
skill_prerequisites: ["c-cpp", "microcontrollers"]
project_prerequisites: ["sensor-logger-with-serial-output.md"]
prerequisite_learning_hours: 4
---

# Bootloader and Firmware Update Mechanism

## Production Workflow Mirrored
1. Partitioning flash into bootloader, application slots, and metadata
2. Receiving a new image over a link and writing it to a staging slot
3. Verifying integrity and authenticity before ever running it
4. Swapping to the new image and rolling back if it fails to boot
5. Making the whole process survive power loss at any moment

## What You'll Build
A bootloader for your board that boots the application from an active
slot, accepts a new firmware image over UART (or the network if your
board has it) into a second slot, verifies a hash and a signature,
marks it pending, boots it once, and confirms or rolls back based on
whether the new application marks itself healthy, with the entire
process tested against power loss at every step.

## Student-Scope Notes
- Writing the bootloader yourself is the exercise. Read how MCUboot
  does it, but implement your own minimal version to understand the
  problems.
- Signing uses a standard algorithm (Ed25519 or ECDSA) via a small
  library; do not implement the cryptography yourself.
- "Network" can be UART with a host script; the update protocol matters
  more than the transport.

## Steps
1. Design the flash layout: bootloader region, two application slots,
   and a metadata sector for slot state (active, pending, confirmed,
   version). Write the linker scripts.
2. Build the minimal bootloader: read metadata, validate the active
   slot's hash, and jump to it with correct vector table relocation.
3. Add the image-receive path: a host script sends an image in chunks
   over UART with a simple acknowledged protocol; the bootloader (or the
   application) writes it to the inactive slot.
4. Add integrity and authenticity: hash the received image, verify a
   signature over the hash with an embedded public key, and reject
   anything that fails. Test with a tampered image.
5. Implement the swap: mark the new slot pending, reboot into it, and
   have the application call a confirm function after its self-check.
6. Implement rollback: if the pending image does not confirm within a
   boot, or the watchdog fires, revert to the previous slot.
7. Test power loss: cut power during receive, during metadata write, and
   during first boot of the new image, and confirm the device always
   boots a valid image. Make metadata updates atomic.
8. Write up the flash layout, the state machine, the security model
   (what the signature does and does not protect against), and the
   power-loss test matrix.

## Extension Ideas
- Add anti-rollback with a monotonic version counter.
- Add delta updates to reduce transfer size.
- Add encryption of the image at rest.
- Add secure boot using the chip's hardware root of trust.

## Skills Demonstrated
- Flash partitioning, linker scripts, and application handoff
- Firmware transfer protocols and staged updates
- Cryptographic verification of firmware
- Fail-safe state machines tested under power loss

## Industry Relevance

Medical Devices, Automotive, Industrial IoT, Consumer Electronics. Field updates are mandatory in these sectors and a bricked device is a recall, so firmware engineers who have built a fail-safe, signed update path are trusted with the most critical part of the product. This is a frequent senior-level interview topic and a rare portfolio piece.
