import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class StateService {
  private lastResult: any = null;
  private currentTopic = '';
  private currentCollection = '';

  setLastResult(r: any)         { this.lastResult = r; }
  getLastResult(): any          { return this.lastResult; }

  setCurrentTopic(t: string)    { this.currentTopic = t; }
  getCurrentTopic(): string     { return this.currentTopic; }

  setCurrentCollection(c: string) { this.currentCollection = c; }
  getCurrentCollection(): string  { return this.currentCollection; }
}
