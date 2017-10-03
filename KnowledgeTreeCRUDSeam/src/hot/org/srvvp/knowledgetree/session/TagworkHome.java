package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("tagworkHome")
public class TagworkHome extends EntityHome<Tagwork> {

	@In(create = true)
	TagworkHome tagworkHome;

	public void setTagworkId(String id) {
		setId(id);
	}

	public String getTagworkId() {
		return (String) getId();
	}

	@Override
	protected Tagwork createInstance() {
		Tagwork tagwork = new Tagwork();
		return tagwork;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public Tagwork getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<Tagwork> getTagworks() {
		return getInstance() == null ? null : new ArrayList<Tagwork>(
				getInstance().getTagworks());
	}
	public List<WorkHasTag> getWorkHasTags() {
		return getInstance() == null ? null : new ArrayList<WorkHasTag>(
				getInstance().getWorkHasTags());
	}

}
