import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private currentCollectionSubject = new BehaviorSubject<string>('');
  public currentCollection$ = this.currentCollectionSubject.asObservable();

  private currentTopicSubject = new BehaviorSubject<string>('');
  public currentTopic$ = this.currentTopicSubject.asObservable();

  constructor() { }

  setCurrentCollection(collectionName: string) {
    this.currentCollectionSubject.next(collectionName);
  }

  getCurrentCollection(): string {
    return this.currentCollectionSubject.value;
  }

  setCurrentTopic(topic: string) {
    this.currentTopicSubject.next(topic);
  }

  getCurrentTopic(): string {
    return this.currentTopicSubject.value;
  }
}
